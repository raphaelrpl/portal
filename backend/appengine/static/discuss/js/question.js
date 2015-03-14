/**
 * Created by raphael on 3/11/15.
 */

var questionModule = angular.module("questionModule", []);

questionModule.directive("questionform", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/form.html',
        scope: {
            question: '='
        },
        controller: function($scope, $http) {
            $scope.publish = function() {
                $http.post('/questions/rest/new', $scope.question).success(function(question) {
                    console.log(question);
                    var html = '<div class="nav-tabs-custom">' +
                            '<ul class="nav nav-tabs pull-right ui-sortable-handle">' +
                                '<li class="pull-left header padding-bottom">' + question.name +'</li>' +
                            '</ul>' +
                            '<div class="publisher">' +
                                '<img src="/static/dist/img/user2-160x160.jpg">' +
                                '<span style="padding-left: 10px;"><b>' + question.user + '</b></span>' +
                                '<span class="pull-right" style="padding-right: 20px;">' + question.creation + '</span>' +
                            '</div>' +
                            '<div class="tab-content">' +
                                '<div class="box-footer clearfix no-border">' +
                                    '<a href="#" class="btn btn-link pull-right"><i class="fa fa-comment margin-icon"></i>Responder</a>' +
                                    '<a href="#" class="btn btn-link pull-right"><i class="fa fa-comment margin-icon"></i>Ver discussão</a>' +
                                    '<a href="#" class="btn btn-link pull-right"><i class="fa fa-fire margin-icon"></i>Recomendar</a>' +
                                '</div>'+
                            '</div>'+
                        '</div>';
                    alert("Cadastrou com sucesso");
                }).error(function(errors) {
                    console.log(errors);
                    alert("Erro ao publicar");
                });
            }
        }
    }
});

questionModule.directive("questionline", function() {
    return {
        restrict: 'A',
        replace: true,
        templateUrl: '/static/discuss/html/question_line.html',
        scope: {
            question: '='
        },
        controller: function($scope, $http) {

        }
    }
});