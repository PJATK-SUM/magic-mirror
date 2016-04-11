import { Meteor } from "meteor/meteor";
import { Template } from 'meteor/templating';
import { ReactiveVar } from 'meteor/reactive-var';
import { Weather } from "/imports/weather.js"

import './main.html';

Template.body.onCreated(function bodyOnCreated() {
  Meteor.subscribe("Weather");
});

Template.body.helpers({
  weathers: function () {
    return Weather.find({}, {sort: {createdAt: -1}, limit: 1})
  }
});
