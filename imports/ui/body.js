import { Meteor } from "meteor/meteor";
import { Template } from 'meteor/templating';

import { Weather } from "/imports/weather.js"
import { News } from "/imports/news.js"

import './body.html';

Template.body.onCreated(function bodyOnCreated() {
  Meteor.subscribe("Weather");
  Meteor.subscribe("News");
});

Template.body.helpers({
  weathers: function () {
    return Weather.find({});
  },
  newsItems: function () {
    return News.find({});
  }
});
