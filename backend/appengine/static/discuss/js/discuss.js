/**
 * Created by raphael on 3/11/15.
 */

var discussModule = angular.module("discussModule", []);

discussModule.directive("discussTag", function() {
    return {
        restrict: 'E',
        replace:true,
        template: ''
    }
});
