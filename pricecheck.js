/**
 * pricecheck.js: an automated price checker for the Steam community market
 *
 * author: Frank Liu - frank.zijie@gmail.com
 * last modified: 05/02/2015
 * 
 * Copyright (c) 2015, Frank Liu
 * All rights reserved. BSD license.
 */

var casper = require("casper").create();
var fs = require("fs");

var OUT_FNAME = "price.tmp";

/**
 * Login to a steam account.
 */
function login() {
    casper.then(function() {
        console.error("Not yet implemented");
    });
}

/**
 * Gets the price of a particular weapon+skin combo in USD.
 */
function getPrice(weap, skin, wear) {

    casper.thenOpen("http://steamcommunity.com/markest/search", function() {
        var query = "\"" weap + "|" + skin + "(" + wear + ")" + "\"";
        casper.sendKeys("#findItemsSearchBox", query);
        casper.click("#findItemsSearchSubmit");
    });

    casper.waitForSelector("#result_0", function() {
        fs.write(OUT_FNAME, casper.getHTML("#result_0"), "w");
    });

}

casper.start("http://steamcommunity.com/market", function() {

    var weap = casper.cli.get("weapon");
    var skin = casper.cli.get("skin");
    var wear = casper.cli.get("wear");
    getPrice(weap, skin, wear);

});

casper.run();
