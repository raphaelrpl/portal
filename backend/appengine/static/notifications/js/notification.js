var notificationModule = angular.module('notificationModule', []);

function get_notifications($scope, $http) {
    $http.post($scope.postUrl, {}).success(function(data) {
        $scope.notifications = [];
        angular.forEach(data, function(k, v){
            if (k.sender.id != $scope.loggedUser) {
                $scope.notifications.push(k);
            }
        });
        console.log(data);
    }).error(function(errors) {
        $scope.errors = errors;
        console.log($scope.errors);
    });
}

notificationModule.directive("notification", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/notifications/html/notification.html',
        scope: {
            postUrl: '@',
            notificationUrl: '@',
            loggedUser: '@'
        },
        controller: function($scope, $http) {
            $scope.errors = {};
            $scope.notifictions = [];
            $scope.notificationsRead = [];
            get_notifications($scope, $http);
        }
    }
});

notificationModule.directive("notificationList", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/notifications/html/list.html',
        scope: {
            postUrl: '@'
        },
        controller: function($scope, $http) {
            $scope.notifications = [];
            get_notifications($scope, $http);
        }
    }
});