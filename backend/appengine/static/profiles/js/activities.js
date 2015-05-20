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
            $scope.getter = function(data) {
                console.log('GETTER');
                console.log(data);
            }
        }
    };
});