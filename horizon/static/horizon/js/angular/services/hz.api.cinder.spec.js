/*
 *    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

(function() {
  'use strict';

  describe('Cinder API', function() {
    var service;
    var apiService = {};
    var toastService = {};

    beforeEach(module('hz.api'));

    beforeEach(module(function($provide) {
      window.apiTest.initServices($provide, apiService, toastService);
    }));

    beforeEach(inject(['hz.api.cinder', function(cinderAPI) {
      service = cinderAPI;
    }]));

    it('defines the service', function() {
      expect(service).toBeDefined();
    });

    var tests = [
      { func: 'getVolumes',
        method: 'get',
        path: '/api/cinder/volumes/',
        data: { params: 'config' },
        error: 'Unable to retrieve the volumes.',
        testInput: [ 'config' ] },

      { func: 'getVolumes',
        method: 'get',
        path: '/api/cinder/volumes/',
        data: {},
        error: 'Unable to retrieve the volumes.' },

      { func: 'getVolumeSnapshots',
        method: 'get',
        path: '/api/cinder/volumesnapshots/',
        data: {},
        error: 'Unable to retrieve the volume snapshots.' },

      { func: 'getVolumeSnapshots',
        method: 'get',
        path: '/api/cinder/volumesnapshots/',
        data: { params: 'config' },
        error: 'Unable to retrieve the volume snapshots.',
        testInput: [ 'config' ] } ] ;

    // Iterate through the defined tests and apply as Jasmine specs.
    angular.forEach(tests, function(params) {
      it('defines the ' + params.name + ' call properly', function() {
        var callParams = [apiService, service, toastService, params];
        window.apiTest.testCall.apply(this, callParams);
      });
    });

  });
})();
