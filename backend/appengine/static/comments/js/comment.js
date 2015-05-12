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
            $scope.submitting = false;

            $scope.sendComment = function() {
                $scope.submitting = true;
                $http.post($scope.postUrl, $scope.comment).success(function(question) {
                    $scope.comment.content = "";
                    console.log(question);
                    $scope.commentList.unshift(question);

                }).error(function(errors) {
                    $scope.errors = errors;
                    console.log($scope.errors);
                }).then(function(done){
                    $scope.submitting = false;
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
                    $scope.editing = false;
                }).error(function(e) {
                    $scope.editing = true;
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
                        if (key.id == data.id) {
                            $scope.commentList.splice(key, 1);
                            console.log("Removeu");
                        }
                    });
                }).error(function(e){
                    console.log(e);
                });
            }
        },
        link: function(scope, element, attr){
            scope.updateFn = function (comment) {
                scope.submitEdit(comment);
            };

            scope.deleteFn = function (comment) {
                console.log(comment);
                scope.submitDelete(comment);
            }
        }
    }
});