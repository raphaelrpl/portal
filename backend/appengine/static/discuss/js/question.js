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
            $scope.publish = function() {
                $http.post('/discuss/', $scope.question).success(function() {

                });
            }
        }
    }
});