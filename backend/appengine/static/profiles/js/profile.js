var profileModule = angular.module("profileModule", ['activityModule']);

profileModule.directive("profile", function () {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/profiles/html/profile.html',
        scope: {
            profile: '=',
            loggedUser: '=',
            postUrl: '='
        },
        controller: function ($scope, $http) {
            $scope.submitting = false;
            $scope.editing = false;
            $scope.errors = {};
            $scope.activities = [];

            $scope.changeToEdit = function () {
                $scope.editing = true;
                $scope.newProfile = JSON.parse(JSON.stringify($scope.profile));
                console.log($scope.newProfile);
            };

            $scope.submitEdit = function (newProfile) {
                console.log(newProfile);
                $scope.submitting = true;
                $http.post($scope.postUrl, newProfile).success(function (data) {
                    console.log("FOI");
                    console.log(data);
                    $scope.profile = data;
                    $scope.editing = false;
                }).error(function (e) {
                    console.log("NUM FOI");
                    console.log(e);
                    $scope.errors = e;
                    if (e.user)
                        alert("You must be logged");
                }).finally(function () {
                    $scope.submitting = false;
                });
            }
        }
    };
});