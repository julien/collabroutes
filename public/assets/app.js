'use strict';

var app;
app = angular.module('colabroutes', []);

app.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'home-tpl',
      controller: 'HomeCtrl',

      resolve: {
        // get our offers before showing
        // the view
        user: function ($q, $http) {
          var defer = $q.defer();
          $http.get('/user').success(function (data) {
            defer.resolve(data);
          });        
          return defer.promise;
        },

        offers: function ($q, $http) {
          var defer = $q.defer();
          $http.get('/offer').success(function (data) {
            defer.resolve(data);
          });
          return defer.promise;
        }
      }
    });
});

// controllers
app.controller('AppCtrl', function ($rootScope) {

});

app.controller('HomeCtrl', function ($scope, $http, user, offers) {
  $scope.user = user;
 
  $scope.handleSubmit = function (e) {
    console.log('ok', e, $scope.data.origin);
  };
});

app.directive('searchBar', function () {
  return {
    restrict: 'E',
    
    template: 
      '<form class="inline" ng-submit="handleSubmit()">' + 
        '<div class="row">' +
          '<div class="small-12">' + 
            '<div class="row">' +
              '<div class="small-3 columns">' + 
                '<input type="text" ng-model="data.origin" placeholder="origin"></input>' + 
              '</div>' +
              '<div class="small-3 columns">' +
                '<input type="text" ng-model="destination" placeholder="destination"></input>' +
              '</div>' +
              '<div class="small-6 columns">' +
                 '<input type="submit" class="button" value="ok">' +
              '</div>' +
            '</div>' + 
          '</div>' +
        '</div>' +
      '</form>',
    
    
    link: function (scope, element, attrs) {
          
    }

  };
});
