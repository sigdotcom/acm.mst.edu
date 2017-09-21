'use strict';

var gulp = require('gulp');
var glob = require('glob');
var sass = require('gulp-sass');

gulp.task('glob', () => {
    // glob search for scss files
    glob('./ACM_General/*/static/*/scss/*.scss', (er, files) => {
        files.forEach( (file) => {
            // remove file and scss directory from path
            var path = file.split('/').slice(0,-2).join('/');
            // add css directory to path
            path = path + '/css/'
            gulp.src(file)
              .pipe(sass())
              .pipe(gulp.dest(path))
        });
    });
});

// gulp start point
gulp.task('default', ['glob']);

