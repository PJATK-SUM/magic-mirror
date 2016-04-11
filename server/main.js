import { Meteor } from 'meteor/meteor';
import { Weather } from "/imports/weather.js";
import { WeatherService } from "/imports/weather_service.js";

Meteor.startup(() => {
    WeatherService.fetchWeather();
    Meteor.setInterval(WeatherService.fetchWeather, 3600000);
  Meteor.publish("Weather", function () {
    return Weather.find({});
  });
});
