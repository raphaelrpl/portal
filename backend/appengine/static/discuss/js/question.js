/**
 * Created by raphael on 3/11/15.
 */

var questionModule = angular.module("questionModule", ['recommendationModule']);

questionModule.directive("questionform", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/form.html',
        scope: {
            question: '=',
            categorysSelected: '='
        },
        controller: function($scope, $http) {
            $scope.errors = {};

            $scope.publish = function() {
                var cat = $scope.categorysSelected[0];
                if (!cat)
                    alert("Selecione ao menos uma categoria");
                $http.post('/questions/rest/new', {categorys: cat, question: $scope.question}).success(function(question) {
                //$http.post('/questions/rest/new', $scope.question).success(function(question) {
                    console.log(question);
                    window.location = "/questions";
                }).error(function(errors) {
                    $scope.errors = errors;
                });
            }
        }
    }
});

questionModule.directive("question", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/question.html',
        scope: {
            question: '=',
            loggedUser: '=',
            questions: '='
        },
        controller: function($scope, $http) {
            $scope.editing = false;
            $scope.submitting = false;

            $scope.updateFn = function(question) {
                $scope.submitting = true;
                $http.post("/questions/rest/edit", question).success(function(data){
                    console.log("Question Alterada");
                    $scope.editing = false;
                }).error(function(e){
                    console.log("Erro Alterar Question");
                }).finally(function(d) {
                    $scope.submitting = false;
                });
            };

            $scope.deleteFn = function(question) {
                console.log("Deletando");
                $scope.submitting = true;
                $http.post("/questions/rest/delete/" + question.id, {}).success(function(data){
                    console.log("Question Deletada");
                    $scope.editing = false;
                    angular.forEach($scope.questions, function(key, value) {
                        if (key.id == data.id) {
                            $scope.questions.splice(key, 1);
                            console.log("Removeu");
                        }
                    });
                }).error(function(e){
                    console.log("Erro Deletar Question");
                }).finally(function(d) {
                    $scope.submitting = false;
                });
            }
        }
    }
});