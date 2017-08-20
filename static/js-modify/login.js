require("../../bower_components/angular/angular.js");
jQuery = require("../../bower_components/jquery/dist/jquery.js");
require("../../bower_components/bootstrap/dist/js/bootstrap.js");
loginCtrl = angular.module('app',[]).controller('loginCtrl',['$scope',function($scope){
    $scope.user = {
        loginName : "",
        password : ""
    };
    $scope.login = function() {
        jQuery.post("/sys/login/",$scope.user,function(data){
            if(data.error_no == "0") {
                location.href = "/index.html";
            }
            else {
                alert(data.data.message);
            }
        });
    };
}]);
loginCtrl.$inject = ['$scope','loginCtrl'];
