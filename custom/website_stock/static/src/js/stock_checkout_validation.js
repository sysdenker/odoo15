odoo.define('website_stock.stock_checkout_validation', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');


    var _t = core._t;
    var temp = '1';


    publicWidget.registry.websiteSaleCart.include({
        events: {
            'click .js_change_shipping': '_onClickChangeShipping',
            'click .js_edit_address': '_onClickEditAddress',
            'click .js_delete_product': '_onClickDeleteProduct',
            'click .remove-cart-line': '_onRemoveCartLine',
            'change .js_quantity': '_onCartQuantity',
        },
        _onRemoveCartLine: function (ev) {
            var $dom = $(ev.currentTarget).closest('td');
            var line_id = parseInt($dom.data('line-id'), 10);
            var product_id = parseInt($dom.data('product-id'), 10);
            ajax.jsonRpc("/shop/cart/update_json", 'call', {
                'line_id': line_id,
                'product_id': product_id,
                'set_qty': 0.0
            })
            .then(function(data) {
                var $q = $(".my_cart_quantity");
                $q.parent().parent().removeClass("hidden", !data.quantity);
                $q.html(data.cart_quantity).hide().fadeIn(600);
                location.reload();
            });
        },
        _onCartQuantity: function (ev) {
            var $input = $(ev.currentTarget);
            var value = parseInt($input.val(), 10);
            var $dom = $(ev.currentTarget).closest('tr');
            var line_id = parseInt($input.data('line-id'), 10);
            var product_id = parseInt($input.data('product-id'), 10);
            ajax.jsonRpc("/shop/cart/update_json/msg", 'call', {
                'line_id': line_id,
                'product_id': parseInt($input.data('product-id'), 10),
                'set_qty': value
            })
            .then(function(msg) {
                console.log(msg);
                if (msg) {
                    console.log("test1"+msg);
                    $dom.popover({
                        content: _t("You are Trying to Add More Than Available Quantity of Product."),
                        title: _t("WARNING"),
                        placement: "top",
                        trigger: 'focus',
                    });
                    $dom.popover('show');
                    setTimeout(function() {
                        $dom.popover('dispose')
                    }, 700);
                } else {
                    $dom.popover('dispose');
                }
            });
        },

    });

    publicWidget.registry.productsRecentlyViewedUpdate.include({
        init: function () {
            return this._super.apply(this, arguments);
        },
        _updateProductView: function () {
            // alert();
            return this._super.apply(this, arguments);
        },
        
    });

});


/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* Responsible Developer:- Sunny Kumar Yadav */
