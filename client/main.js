import S from "string";
import moment from "moment";

import { Meteor } from "meteor/meteor";
import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Weather } from "/imports/weather.js"
import { News } from "/imports/news.js"

import './main.html';

Template.body.onCreated(function bodyOnCreated() {
  Meteor.subscribe("Weather");
  Meteor.subscribe("News");
});

Template.body.helpers({
  weathers: function () {
    return Weather.find({}, {sort: {createdAt: -1}, limit: 1});
  },
  newsItems: function () {
    return News.find({}, {sort: {publishedAt: -1}, limit: 4});
  }
});

Template.news.helpers({
  truncate: function (text) {
    if (text) {
      return S(text).truncate(500);
    } else {
      return "";
    }
  },
  newsDate: function (date) {
    return moment(date).format("DD.MM.YYYY");
  }
});
