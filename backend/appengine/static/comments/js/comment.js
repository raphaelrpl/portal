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
            loggedUser: '=',
            commentList: '='
        },
        controller: function($scope, $http) {
            $scope.editting = false;
            $scope.errors = {};

            $scope.submitEdit = function(comment) {
                $http.post("/comments/rest/edit", comment).success(function(data) {
                    alert("Alterado");
                    console.log(data);
                }).error(function(e) {
                    $scope.errors = e;
                    console.log("ERROU");
                    console.log($scope.errors);
                });
            };

            $scope.submitDelete = function(comment) {
                console.log(comment);
                var form = new FormData();
                form.append("id", comment.id);
                form.append("user", comment.user);
                $http.post(comment.delete_path, form).success(function(data) {
                    console.log(data);
                    angular.forEach($scope.commentList, function(key, value) {
                        if (value.id == data.id) {
                            $scope.commentList.splice(key, 1);
                            console.log("REMOVeU");
                        }
                    });
                }).error(function(e){
                    console.log(e);
                });
            }
        },
        link: function(scope, element, attr){
            scope.updateFn = function (comment) {
                console.log(comment);
                scope.submitEdit(comment);
            };

            scope.deleteFn = function (comment) {
                console.log(comment);
                scope.submitDelete(comment);
            }
        }
    }
});