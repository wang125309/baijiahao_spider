var gulp = require('gulp');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var jshint = require('gulp-jshint');
var stylus = require('gulp-stylus');
var uglify = require('gulp-uglify');
var jade = require('gulp-jade');
var base64 = require('gulp-base64');
var css_minify = require('gulp-minify-css');
var browserify = require('gulp-browserify');

gulp.task('lint',function(){
    gulp.src('./static/js-modify/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('stylus',function(){
    gulp.src('./static/stylus/*.styl')
        .pipe(stylus())
        .pipe(css_minify())
        .pipe(base64())
        .pipe(gulp.dest('./static/css'));
});

gulp.task('stylus-b',function(){
    gulp.src('./static/css-modify/backend/*.styl')
        .pipe(stylus())
        .pipe(css_minify())
        .pipe(base64())
        .pipe(gulp.dest('./static/css/backend'));
});

gulp.task('js-only',function(){
        gulp.src('./static/js-modify/guide.js')
			.pipe(browserify())
            .pipe(gulp.dest('./static/js'));
});

gulp.task('js',function(){
        gulp.src('./static/js-modify/*.js')
			.pipe(browserify())
            .pipe(gulp.dest('./static/js'));    
});


gulp.task('jsb',function(){
    gulp.src('./static/js-modify/backend/*.js')

        .pipe(browserify())
        .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('js-c',function(){
    gulp.src('./static/js-modify/*.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js'));    
});


gulp.task('jsb-c',function(){
    gulp.src('./static/js-modify/backend/*.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('jsb-backend-order-list',function(){
    gulp.src(['./static/js-modify/backend/spot-order.js',
        './static/js-modify/backend/spot-order-list.js',
        './static/js-modify/backend/hotel-order.js',
        './static/js-modify/backend/hotel-order-list.js',
        './static/js-modify/backend/specailoffer-order.js',
        './static/js-modify/backend/specailoffer-order-list.js',
        './static/js-modify/backend/theme-order.js',
        './static/js-modify/backend/theme-order-list.js'])
    .pipe(browserify())
    // .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('jsb-themeorder',function(){
    gulp.src('./static/js-modify/backend/theme-order.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('jsb-themeorder-list',function(){
    gulp.src('./static/js-modify/backend/theme-order-list.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('jsb-hotelorder',function(){
    gulp.src('./static/js-modify/backend/hotel-order.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('jsb-spotorder',function(){
    gulp.src('./static/js-modify/backend/spot-order.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('jsb-spotorder-list',function(){
    gulp.src('./static/js-modify/backend/spot-order-list.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});

gulp.task('jsb-specailofferorder',function(){
    gulp.src('./static/js-modify/backend/specailoffer-order.js')
    .pipe(browserify())
    .pipe(uglify())
    .pipe(gulp.dest('./static/js/backend'))
});



gulp.task('jade',function(){
    gulp.src('./template/jade/*.jade')
    .pipe(jade())
    .pipe(gulp.dest('./template/'))
});

gulp.task('jb',function(){
    gulp.src('./template/jade/backend/*.jade')
    .pipe(jade())
    .pipe(gulp.dest('./template/backend/'))
});

gulp.task('jade-admin',function(){
    gulp.src('./template/jade/admin/*.jade')
    .pipe(jade())
    .pipe(gulp.dest('./template/admin/'))
});

