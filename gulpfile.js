'use strict';

// Required package list
var gulp = require('gulp');
var glob = require('glob');
var sass = require('gulp-sass');


/*
  Compile each scss file within the `./ACM_General` directory and then
  save the corresponding css file created into a css folder with the
  same path as the scss folder.

  :param string glob: A string containing the name of the operation
    expected handled by gulp.

  :Param lambda (): A glob search operation.
*/
gulp.task('glob', () => {
    // glob search for scss files
    glob('./ACM_General/*/static/*/scss/*.scss', (er, files) => {
        // for each file in the path
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

/*
  Starting point from which all gulp tasks are  ran sequentially.

  :param string task: The default starting task

  :param list tasks: List of task names to be ran in given order.
*/
gulp.task('default', ['glob']);

