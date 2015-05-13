/**
 * Created by raphael on 3/11/15.
 */

var discussModule = angular.module("discussModule", ['recommendationModule']);

discussModule.directive("discussform", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/discuss_form.html',
        scope: {
            discuss: '=',
            uploadUrl: '='
        },
        controller: function($scope, $http) {
            $scope.errors = {};
            $scope.filesChanged = function (elm) {
                console.log(elm);
                $scope.discuss.file = elm.files[0];
                $scope.$apply();
            };
            $scope.publish = function() {
                console.log($scope.uploadUrl);
                $http.post($scope.uploadUrl.url, $scope.discuss, {headers: {'Content-Type': 'multipart/form-data'}}).success(function(question) {
                    console.log(question);
                    alert("FOI");
                    //window.location = "/";
                }).error(function(errors) {
                    $scope.errors = errors;
                    console.log($scope.errors);
                });
            }
        }
    }
});

discussModule.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

discussModule.directive("discuss", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/discuss.html',
        scope: {
            discuss: '=',
            loggedUser: '=',
            discusses: '='
        },
        controller: function($scope, $http) {
            $scope.editing = false;
            $scope.submitting = false;
            $scope.errors = null;

            $scope.updateFn = function(discuss) {
                $scope.submitting = true;
                $http.post("/discusses/rest/edit", discuss).success(function(data){
                    console.log("Discuss Alterada");
                    $scope.editing = false;
                    $scope.errors = null;
                }).error(function(e){
                    $scope.errors = e;
                    console.log("Erro Discuss Question");

                }).finally(function(d) {
                    $scope.submitting = false;
                });
            };

            $scope.deleteFn = function(discuss) {
                console.log("Deletando");
                $scope.submitting = true;
                $http.post("/discusses/rest/delete/" + discuss.id, {}).success(function(data){
                    console.log("Discuss Deletada");
                    $scope.editing = false;
                    $scope.discusses.splice($scope.discusses.indexOf(discuss), 1);
                }).error(function(e){
                    console.log("Erro Deletar Discuss");
                }).finally(function(d) {
                    $scope.submitting = false;
                });
            }
        }
    }
});