var commentModule = angular.module('commentModule', []);

commentModule.directive("docomment", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/comments/html/comment.html',
        scope: {
            comment: '=',
            postUrl: '@'
        },
        controller: function($scope, $http) {
            $scope.errors = {};
            $scope.sendComment = function() {
                $http.post($scope.postUrl, $scope.comment).success(function(question) {
                    console.log(question);
                    alert("FOI");
                    //window.location = "/";
                }).error(function(errors) {
                    $scope.errors = errors;
                });
            }
        }
    }
});

commentModule.directive("usercomment", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/comments/html/user_comment.html',
        scope: {
            comment: '='
        },
        controller: function($scope, $http) {

        }
    }
});