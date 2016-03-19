Weather = new Mongo.Collection("weather");

if (Meteor.isClient) {
  Meteor.subscribe("weather");

  Template.body.helpers({
    weathers: function () {
      return Weather.find({}, {sort: {createdAt: -1}, limit: 1})
    }
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    WeatherService.fetchWeather();
    Meteor.setInterval(WeatherService.fetchWeather, 3600000);
  });
  Meteor.publish("weather", function () {
    return Weather.find({});
  });
}
