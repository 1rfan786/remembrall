var app = angular.module('rememberall', []);

app.controller('MainPanelCtrl', function($scope, testDataFactory) {
  $scope.journal = testDataFactory.journal;

  $scope.coverStyle = function(fileURL) {
    if(!(typeof fileURL === 'undefined')) {
      return {
        'background-image': 'url(' + fileURL + ')',
        'background-size': 'cover'
      };
    }
  };
});

app.controller('SideBarCtrl', function($scope) {
  $scope.feeling = 'happy';
});

app.factory('testDataFactory', function() {
  return { 
    journal: [
      {title: 'entry0', thumbnail: '../media/photo.JPG',
       content: [{type: 'video', value: 'clip.mp4'}, {type: 'text', value: 'my paragraph'}]},
      {title: 'entry2', thumbnail: '../media/photo2.JPG',
       content: [{type: 'text', value: 'one fish'},
                 {type: 'video', value: 'clip2.mp4'}, 
                 {type: 'text', value: 'two fish'}]},
      {title: 'entry3', thumbnail: '../media/photo3.png'},
      {title: 'entry1'},
      {title: 'entry4', thumbnail: '../media/photo4.jpg'},
      {title: 'entry5'},
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
