var commentModule = angular.module('commentModule', []);

commentModule.directive("docomment", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/comments/html/comment.html',
        scope: {
            comment: '=',
            postUrl: '@',
            commentList: '='
        },
        controller: function($scope, $http) {
            $scope.errors = {};
            console.log($scope.commentList);
            $scope.sendComment = function() {
                $http.post($scope.postUrl, $scope.comment).success(function(question) {

                    console.log(question);
                    $scope.commentList.unshift(question);

                }).error(function(errors) {
                    $scope.errors = errors;
                    console.log($scope.errors);
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
            comment: '=',
            loggedUser: '='
        },
        controller: function($scope, $http) {
            editting = false;
        }
    }
});