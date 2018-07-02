(function () {
    'use strict';

    angular
        .module('saturnApp')
        .controller('SaturnVaultController', SaturnVaultController);

    SaturnVaultController.$inject = ['$scope', '$state', 'SaturnVault', 'ParseLinks', 'AlertService', 'paginationConstants', 'pagingParams'];

    function SaturnVaultController($scope, $state, SaturnVault, ParseLinks, AlertService, paginationConstants, pagingParams) {
        var vm = this;

        vm.loadPage = loadPage;
        vm.predicate = pagingParams.predicate;
        vm.reverse = pagingParams.ascending;
        vm.transition = transition;
        vm.itemsPerPage = paginationConstants.itemsPerPage;
        vm.toggleVisible = toggleVisible;
        vm.exportPasswords = exportPasswords;
        vm.clickToCopy = clickToCopy;
        vm.copySuccessText = "Password was successfully copied!"
        vm.copyErrorText = "There was an error copying the password!"


        loadAll();

        function loadAll() {
            SaturnVault.query({
                page: pagingParams.page - 1,
                size: vm.itemsPerPage,
                sort: sort()
            }, onSuccess, onError);
            function sort() {
                var result = [vm.predicate + ',' + (vm.reverse ? 'asc' : 'desc')];
                if (vm.predicate !== 'id') {
                    result.push('id');
                }
                return result;
            }

            function onSuccess(data, headers) {
                vm.links = ParseLinks.parse(headers('link'));
                vm.totalItems = headers('X-Total-Count');
                vm.queryCount = vm.totalItems;
                vm.saturnPasses = data;
                vm.page = pagingParams.page;
            }

            function onError(error) {
                AlertService.error(error.data.message);
            }
        }

        function clickToCopy(passToCopy) {
			var body = angular.element(document.body);
			var textarea = angular.element('<textarea/>');
			textarea.css({
				display: 'hidden',
				position: 'fixed',
				opacity: '0'
			});

			textarea.val(passToCopy);
			body.append(textarea);
			textarea[0].select();
			if (document.execCommand('copy')) {
                AlertService.success(vm.copySuccessText)
			} else {
                AlertService.error(vm.copyErrorText);
            }
		}

        function loadPage(page) {
            vm.page = page;
            vm.transition();
        }

        function toggleVisible(id) {
            //TODO show password and change eye icon
        }

        function transition() {
            $state.transitionTo($state.$current, {
                page: vm.page,
                sort: vm.predicate + ',' + (vm.reverse ? 'asc' : 'desc'),
                search: vm.currentSearch
            });
        }

        function exportPasswords(exportAll) {
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "site,login,password\r\n";
            vm.saturnPasses.forEach(function(saturnPass) {
                if (exportAll || saturnPass.checked) {
                    csvContent += saturnPass.site + ",";
                    csvContent += saturnPass.login + ",";
                    csvContent += saturnPass.password + "\r\n";
                }
            });

            var encodedUri = encodeURI(csvContent);
            var link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "saturn_export.csv");
            document.body.appendChild(link); // Required for FF
            link.click();   // download csv file
            document.body.removeChild(link);
        }
    }
})();
