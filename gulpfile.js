/* jshint esversion: 6 */

var gulp = require("gulp");
var release = require("release-it");
var pypi = require("pypi-release");

function releaseFn( increment ) {
    release.execute( {
        "increment" : increment,
        "non-interactive" : true
    } );
    pypi().then( () => null );
}

gulp.task( "patch", () => releaseFn( "patch" ) );
gulp.task( "minor", () => releaseFn( "minor" ) );
gulp.task( "major", () => releaseFn( "major" ) );
