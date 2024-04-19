odoo.define('mail.DnkAttachmentBox', function (require) {
"use strict";


console.log('111XXX');

var DnkAbstractField = require('web.AbstractField');
var session = require('web.session');
var DnkAbstractFieldBinary = DnkAbstractField.include({

  init: _.extend(DnkAbstractField.prototype.init, {
    this.max_upload_size = 3 * 1024 * 1024;
  )}


  return DnkAbstractFieldBinary

});
