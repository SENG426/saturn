(function () {
	'use strict';

	angular
		.module('saturnApp')
		.controller('SaturnVaultDialogController', SaturnVaultDialogController);

	SaturnVaultDialogController.$inject = ['$timeout', '$scope', '$stateParams', '$uibModal', '$uibModalInstance', 'entity', 'SaturnVault', 'User'];

	function SaturnVaultDialogController($timeout, $scope, $stateParams, $uibModal, $uibModalInstance, entity, SaturnVault, User) {
		var vm = this;

		vm.saturnPass = entity;
		vm.datePickerOpenStatus = {};
		vm.openCalendar = openCalendar;
		vm.openPwdGenModal = openPwdGenModal;
		vm.checkPasswordStrength = checkPasswordStrength;
		vm.passwordStrength = '';
		vm.save = save;
		vm.clear = clear;
		vm.users = User.query();
		vm.pwdVisible = false;

		$timeout(function () {
			angular.element('.form-group:eq(1)>input').focus();
		});

		function openPwdGenModal() {
			$uibModal.open({
				templateUrl: 'app/entities/saturn-vault/saturn-vault-pwd-gen.html',
				controller: 'SaturnVaultPwdGenController',
				controllerAs: 'vm',
				backdrop: 'static',
				size: 'sm'
			}).result.then(function (password) {
				vm.saturnPass.password = password;
				vm.checkPasswordStrength();
			}, function () {
			});
		}

		function calculateLog(value, length, base) {
			return Math.log(Math.pow(value, length))/Math.log(base);
		}

		function checkPasswordStrength() {
			let pool = 0;
			let progress = document.querySelector('.progress');
			
			if(!vm.saturnPass.password) {
				progress.style.display = 'none';
				vm.saturnPass.password = '';
				pool = 0;
				return ;
			}

			if((/[a-z]/.test(vm.saturnPass.password))) {
				pool += 26;
			}

			if((/[A-Z]/.test(vm.saturnPass.password))) {
				pool += 26;
			}

			if((/[0-9]/.test(vm.saturnPass.password))) {
				pool += 10;
			}

			if((/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(vm.saturnPass.password))) {
				pool += 30;
			}
																																																			
			let entropy = calculateLog(pool, vm.saturnPass.password.length, 2);
			let bar = document.querySelector('.progress-bar');
			progress.style.display = 'block';

			if(entropy < 36) {
				vm.passwordStrength = 'weak';
				bar.style.width = '33.3%';
				bar.style.backgroundColor = 'red';

			} else if(entropy >= 36 && entropy < 60) {
				vm.passwordStrength = 'intermediate';
				bar.style.width = '66.6%';
				bar.style.backgroundColor = 'orange';
			} else {
				vm.passwordStrength = 'strong';
				bar.style.width = '100%';
				bar.style.backgroundColor = 'green';
			}
		}

		function clear() {
			$uibModalInstance.dismiss('cancel');
		}

		function save() {
			vm.isSaving = true;
			if (vm.saturnPass.id !== null) {
				SaturnVault.update(vm.saturnPass, onSaveSuccess, onSaveError);
			} else {
				SaturnVault.save(vm.saturnPass, onSaveSuccess, onSaveError);
			}
		}

		function onSaveSuccess(result) {
			$scope.$emit('saturnApp:SaturnVaultUpdate', result);
			$uibModalInstance.close(result);
			vm.isSaving = false;
		}

		function onSaveError() {
			vm.isSaving = false;
		}

		vm.datePickerOpenStatus.createdDate = false;
		vm.datePickerOpenStatus.lastModifiedDate = false;

		function openCalendar(date) {
			vm.datePickerOpenStatus[date] = true;
		}
	}
})();
