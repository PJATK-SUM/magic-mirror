import S from "string";
import moment from "moment";

import { Meteor } from "meteor/meteor";
import { Template } from 'meteor/templating';

import "../imports/ui/body.js";

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
