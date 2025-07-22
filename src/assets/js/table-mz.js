'use strict';

let fv, offCanvasEl;
document.addEventListener('DOMContentLoaded', function(e) {
  const formAddNewRecord = document.getElementById('form-add-new-record');

  setTimeout(() => {
    const newRecord = document.querySelector('.create-new'),
      offCanvasElement = document.querySelector('#add-new-record');

    if (newRecord) {
      newRecord.addEventListener('click', function() {
        offCanvasEl = new bootstrap.Offcanvas(offCanvasElement);
        offCanvasElement.querySelectorAll('input').forEach(i => i.value = '');
        offCanvasEl.show();
      });
    }
  }, 200);

  // اگر فرم add جدیدی هنوز استفاده میشه:
  if (formAddNewRecord) {
    fv = FormValidation.formValidation(formAddNewRecord, {
      fields: {
        basicFullname: {
          validators: {
            notEmpty: { message: 'عنوان الزامی است' }
          }
        },
        basicPost: {
          validators: {
            notEmpty: { message: 'فیلد سمت الزامی است' }
          }
        },
        basicEmail: {
          validators: {
            notEmpty: { message: 'ایمیل الزامی است' },
            emailAddress: { message: 'فرمت ایمیل نادرست است' }
          }
        },
        basicDate: {
          validators: {
            notEmpty: { message: 'تاریخ عضویت الزامی است' },
            date: {
              format: 'MM/DD/YYYY',
              message: 'فرمت تاریخ نادرست است'
            }
          }
        },
        basicSalary: {
          validators: {
            notEmpty: { message: 'حقوق پایه الزامی است' }
          }
        }
      },
      plugins: {
        trigger: new FormValidation.plugins.Trigger(),
        bootstrap5: new FormValidation.plugins.Bootstrap5({
          eleValidClass: '',
          rowSelector: '.col-sm-12'
        }),
        submitButton: new FormValidation.plugins.SubmitButton(),
        autoFocus: new FormValidation.plugins.AutoFocus()
      },
      init: instance => {
        instance.on('plugins.message.placed', function(e) {
          if (e.element.parentElement.classList.contains('input-group')) {
            e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
          }
        });
      }
    });

    const flatpickrDate = document.querySelector('[name="basicDate"]');
    if (flatpickrDate) {
      flatpickrDate.flatpickr({
        enableTime: false,
        dateFormat: 'Y/m/d',
        locale: 'fa',
        onChange: function() {
          fv.revalidateField('basicDate');
        }
      });
    }
  }
});

$(function() {
  const dt_basic_table = $('.datatables-basic');
  let dt_basic;

  if (dt_basic_table.length) {
    dt_basic = dt_basic_table.DataTable({
      ajax: {
        url: '/api/get_all_server_test',
        dataSrc: '' // چون API شما آرایه خالص می‌ده
      },
      columns: [
        {
          data: null,
          orderable: false,
          searchable: false,
          render: function(data, type, row, meta) {
            return `<input type="checkbox" class="dt-checkboxes form-check-input" data-index="${meta.row}">`;
          }
        },
        {
          data: 'country',
          title: 'کشور',
          render: function(data, type, row) {
            return `
        <img alt="${data}" src="/static/img/flag/${data}.png" width="32" class="me-1" style="vertical-align: middle;">
      `;
          }
        },
        { data: 'name', title: 'نام سرور' },
        { data: 'isp', title: 'ISP' }
      ],
      order: [],
      language: {
        url: assetsPath + 'json/i18n/datatables-bs5/fa.json'
      },
      dom: '<"card-header flex-column flex-md-row"<"head-label text-center"><"dt-action-buttons text-end pt-3 pt-md-0">>t',
      displayLength: 10,
      responsive: true
    });

    $('div.head-label').html('<h5 class="card-title mb-0">انتخاب سرور برای تست</h5>');

    // 🎯 دکمه شروع تست
    $('#testButton').on('click', function() {
      const selectedServers = [];

      dt_basic_table.find('tbody input.dt-checkboxes:checked').each(function() {
        const index = $(this).data('index');
        const rowData = dt_basic.row(index).data();
        if (rowData) selectedServers.push(rowData);
      });

      if (selectedServers.length === 0) {
        return alert('لطفاً حداقل یک سرور را انتخاب کنید.');
      }

      console.log('✅ سرورهای انتخاب‌شده:', selectedServers);

      // 👉 اینجا عملیات بعدی رو انجام بده
      // مثلاً:
      // startTest(selectedServers);
    });
  }
});
