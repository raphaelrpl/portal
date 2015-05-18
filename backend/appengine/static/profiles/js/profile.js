var profileModule = angular.module("profileModule", []);

profileModule.directive("profile", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/profiles/html/profile.html',
        scope: {
            profile: '=',
            loggedUser: '='
        },
        controller: function($scope, $http) {
            console.log("OI");
        }
    };
});