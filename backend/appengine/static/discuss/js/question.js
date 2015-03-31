/**
 * Created by raphael on 3/11/15.
 */

var questionModule = angular.module("questionModule", []);

questionModule.directive("questionform", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/form.html',
        scope: {
            question: '='
        },
        controller: function($scope, $http) {
            $scope.errors = {};
            $scope.publish = function() {
                $http.post('/questions/rest/new', $scope.question).success(function(question) {
                    console.log(question);
                    window.location = "/";
                }).error(function(errors) {
                    $scope.errors = errors;
                });
            }
        }
    }
});

questionModule.directive("questionline", function() {
    return {
        restrict: 'A',
        replace: true,
        templateUrl: '/static/discuss/html/question_line.html',
        scope: {
            question: '='
        },
        controller: function($scope, $http) {

        }
    }
});