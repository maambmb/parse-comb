/* jshint esversion: 6 */

var release = require("release-it");
var pypi = require( "pypi-release" );
var args = require("yargs")
    .alias( "i", "increment" )
    .argv;

var opts = {
    "increment" : args.increment || "patch",
    "non-interactive" : true
};

release.execute( opts )
    .then( pypi );
