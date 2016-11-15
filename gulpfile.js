/*jshint esversion:6*/

var gulp = require("gulp");
var release = require("gulp-release-it");
var fs = require("fs");
var ejs = require("ejs");
var requireUncached = require("require-uncached");
var _ = require('underscore');

release(gulp);

// create a template for the setup.py file
var TEMPLATE = ejs.compile( `
    # auto generated setup.py script - please don't edit directly!
    from setuptools import setup

    setup(
        name = '<%= name %>',
        version = '<%= version %>',
        description = '<%= description %>',
        author_email = '<%= author %>',
        license = '<%= license %>',
        keywords = '<%= keywords.join( " " ) %>'
    )
`);

var DEFAULTS = {
    license : "MIT",
    author : "",
    description : "",
    keywords : []
};

gulp.task( "mk-setup", [ "release" ], function() {
    // load a fresh version of the node package json file
    var pkg = _.extend( {}, DEFAULTS, requireUncached( "./package.json" ) );
    fs.createWriteStream( "setup.py" )
        .end( TEMPLATE( pkg ) );
});
