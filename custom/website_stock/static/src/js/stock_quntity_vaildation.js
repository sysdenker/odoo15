odoo.define('website_stock.stock_quntity_vaildation', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');

    var _t = core._t;
    var temp = '1';
    var publicWidget = require('web.public.widget');
    var VariantMixin = require('sale.VariantMixin');


    var _t = core._t;
    var temp = '1';


    publicWidget.registry.WebsiteSale.include({

        init: function(){
            var $js_quantity = $('.oe_website_sale').find('.css_quantity.input-group.oe_website_spinner');
            this.website_stock_main($js_quantity);
            return this._super.apply(this, arguments);
        },

        website_stock_main:function($js_quantity) {
            if ($("input[name='product_id']").is(':radio'))
                var product = $("input[name='product_id']:checked").attr('value');
            else
                var product = $("input[name='product_id']").attr('value');
            var value = $('#' + product).attr('value');
            var allow = $('#' + product).attr('allow');
            $('.stock_info_div').hide();
            $('#' + product).show();
            if (value <= 0 && allow === 'deny') {
                $('#add_to_cart').hide();
                $js_quantity.hide();
            } else {
                $('#add_to_cart').show();
                $js_quantity.show();
            }
        },

        _onClickAdd: function (ev) {
            ev.preventDefault();
            var $form = $(ev.currentTarget).closest('form');
            if ($("input[name='product_id']").is(':radio'))
                var product_id = $("input[name='product_id']:checked").attr('value');
            else
                var product_id = $("input[name='product_id']").attr('value');
            var add_qty = parseFloat($form.find('input[type="text"][name="add_qty"]').first().val(), 10);
            ajax.jsonRpc("/shop/cart/update/msg", 'call', {
                'product_id': product_id,
                'add_qty': add_qty
            })
            .then(function(result) {
                if (result.status == 'deny') {
                    $form.find('input[type="text"][name="add_qty"]').first().val(temp);
                    $('#add_to_cart').popover({
                        content: _t("You Already Added All Avalible Quantity of Product in Your Cart, You Can not Add More Quantity."),
                        title: _t("WARNING"),
                        placement: "left",
                        trigger: 'focus',
                    });
                    $('#add_to_cart').popover('show');
                    setTimeout(function() {
                        $('#add_to_cart').popover('dispose')
                    }, 1000);

                } else {
                    $('#add_to_cart').popover('dispose');
                    temp = add_qty.toString();
                }
            });
            this.isBuyNow = $(ev.currentTarget).attr('id') === 'buy_now';
            return this._handleAdd($(ev.currentTarget).closest('form'));
        },
        _onChangeAddQuantity: function (ev) {
            var $form = $(ev.currentTarget).closest('form');
            if ($("input[name='product_id']").is(':radio'))
                var product_id = $("input[name='product_id']:checked").attr('value');
            else
                var product_id = $("input[name='product_id']").attr('value');
            var add_qty = parseFloat($form.find('input[type="text"][name="add_qty"]').first().val(), 10);
            ajax.jsonRpc("/shop/cart/update/msg", 'call', {
                'product_id': product_id,
                'add_qty': add_qty
            })
            .then(function(result) {
                if (result.status == 'deny') {
                    $form.find('input[type="text"][name="add_qty"]').first().val(temp);
                    $('.css_quantity').popover({
                        content: _t("You Can Not Add More Quantity."),
                        title: _t("WARNING"),
                        placement: "top",
                        trigger: 'focus',
                    });
                    $('.css_quantity').popover('show');
                    setTimeout(function() {
                        $('.css_quantity').popover('dispose')
                    }, 1000);
                } else {
                    $('.css_quantity').popover('dispose');
                    temp = add_qty.toString();
                }
            });
            this.onChangeAddQuantity(ev);
        },
        // _onInputQty: function (ev) {
        //     var $form = $(ev.currentTarget).closest('form');
        //     var $msg = $form.find('.fa-shopping-cart');
        //     var product_id = parseInt($form.find('input[type="hidden"][name="product_id"]').first().val(), 10);
        //     ajax.jsonRpc("/shop/cart/update/msg", 'call', {
        //         'product_id': product_id,
        //         'add_qty': 1
        //     })
        //     .then(function(result) {
        //         if (result.status == 'deny') {
        //             $(ev.currentTarget).addClass('disabled');
        //             alert(_t("You Can Not Add This Product in Your Cart."))
        //         }
        //     });
        // },

    });

});


/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* Responsible Developer:- Sunny Kumar Yadav */
