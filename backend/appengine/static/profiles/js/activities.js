var activityModule = angular.module("activityModule", []);

activityModule.directive("activity", function () {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/profiles/html/activity.html',
        scope: {
            data: '='
        },
        controller: function ($scope) {
            $scope.redirectPage = function(data) {
                if (data.notification_type == "question") {
                    window.location = "/questions/" + data.post;
                }
                if (data.notification_type == "discuss") {
                    window.location = "/discusses/" + data.post;
                }
            }
        }
    };
});