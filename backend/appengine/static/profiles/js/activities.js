var activityModule = angular.module("activityModule", []);

activityModule.directive("activity", function () {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/profiles/html/activity.html',
        scope: {
            data: '@'
        },
        controller: function ($scope) {

        }
    };
});