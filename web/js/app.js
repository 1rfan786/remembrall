var app = angular.module('rememberall', []);

app.controller('MainPanelCtrl', function($scope, testDataFactory) {
  $scope.savedLib = testDataFactory.savedLib;
});

app.controller('SideBarCtrl', function($scope) {
  $scope.feeling = 'happy';
});

app.factory('testDataFactory', function() {
  return { 
    savedLib: [
      {name: 'entry1', frame: '../media/photo.JPG', video: 'clip.mp4'},
      {name: 'entry2', frame: '../media/photo2.JPG', video: 'clip2.mp4'},
        {name: 'entry3', frame: '../media/photo3.PNG'},
        {name: 'entry4', frame: '../media/photo4.JPG'},
        
    ]
  };
});


app.directive('mainpanel', function() {
  return {
    restrict: 'E',
    templateUrl: '../partials/mainPanel.partial.html'
  };
});

app.directive('sidebar', function() {
  return {
    restrict: 'E',
    templateUrl: '../partials/sideBar.partial.html'
  };
});
