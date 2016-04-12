import { Meteor } from 'meteor/meteor';
import { Weather } from "/imports/weather.js";
import { WeatherService } from "/imports/weather_service.js";
import { News } from "/imports/news.js";
import { NewsService } from "/imports/news_service.js";

Meteor.startup(() => {
  // Weather service setup
  WeatherService.fetchWeather();
  Meteor.setInterval(WeatherService.fetchWeather, 3600000);
  Meteor.publish("Weather", function () {
    return Weather.find({});
  });

  // News service setup
  NewsService.fetchNews();
  Meteor.setInterval(NewsService.fetchNews, 3600000);
  Meteor.publish("News", function () {
    return News.find({});
  });
});
