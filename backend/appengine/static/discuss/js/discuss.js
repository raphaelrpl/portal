/**
 * Created by raphael on 3/11/15.
 */

var discussModule = angular.module("discussModule", []);

discussModule.directive("discussform", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/discuss_form.html',
        scope: {
            discuss: '=',
            uploadUrl: '='
        },
        controller: function($scope, $http) {
            $scope.errors = {};
            $scope.filesChanged = function (elm) {
                console.log(elm);
                $scope.discuss.file = elm.files[0];
                $scope.$apply();
            };
            $scope.publish = function() {
                console.log($scope.uploadUrl);
                $http.post($scope.uploadUrl.url, $scope.discuss, {headers: {'Content-Type': 'multipart/form-data'}}).success(function(question) {
                    console.log(question);
                    alert("FOI");
                    //window.location = "/";
                }).error(function(errors) {
                    $scope.errors = errors;
                    console.log($scope.errors);
                });
            }
        }
    }
});

discussModule.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);
//
//discussModule.directive("inputImage", ['$parse', function($parse){
//    return {
//        restrict: 'A',
//        link: function(scope, elm, attrs) {
//            elm.bind('change', function () {
//                $parse(attrs.inputImage).assign(scope, elm[0].files);
//                scope.$apply();
//            })
//        }
//    }
//}]);