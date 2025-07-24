$(function() {
  const dt_basic_table = $('.datatables-basic');
  const testButton = document.getElementById('testButton');
  let dt_basic;
  let isRunning = false;
  let isRotationActive = false;

  if (dt_basic_table.length) {
    dt_basic = dt_basic_table.DataTable({
      ajax: {
        url: '/api/get_all_server_test',
        dataSrc: ''
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
          render: function(data) {
            return `
              <img alt="${data}" src="/static/img/flag/${data}.png" width="32" class="me-1" style="vertical-align: middle;">
            `;
          }
        },
        { data: 'name', title: 'نام سرور' },

        { data: 'url', title: 'IP' },
        { data: 'isp', title: 'ISP' }
      ],
      language: {
        url: assetsPath + 'json/i18n/datatables-bs5/fa.json'
      },
      order: [],
      responsive: true,
      displayLength: 10,
      dom: '<"card-header flex-column flex-md-row"<"head-label text-center"><"dt-action-buttons text-end pt-3 pt-md-0">>t'
    });

    $('div.head-label').html('<h5 class="card-title mb-0">انتخاب سرور برای تست</h5>');


    testButton.addEventListener('click', function() {
      if (isRunning) return;

      const selectedServers = [];

      dt_basic_table.find('tbody input.dt-checkboxes:checked').each(function() {
        const index = $(this).data('index');
        const rowData = dt_basic.row(index).data();
        if (rowData) selectedServers.push(rowData);
      });

      if (selectedServers.length === 0) {
        alert('لطفاً حداقل یک سرور را انتخاب کنید.');
        testButton.classList.remove('active');
        return;
      }

      const urls = selectedServers.map(server => server.url);

      startSpeedTest(urls);
    });
  }


  async function startSpeedTest(urls) {
    if (isRotationActive) return; // جلوگیری از اجرای مجدد
    isRotationActive = true;
    testButton.classList.add('active');

    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));


    for (const baseUrl of urls) {
      console.log(`📡 در حال تست سرور: ${baseUrl}`);
      const downloadUrl = `http://${baseUrl}/files/testfile.bin`;

      try {
        const fileSizeInBits = 20971520 * 8;
        const startTime = performance.now();

        const response = await fetch(downloadUrl, { cache: 'no-store' }); // cache: 'no-store' برای جلوگیری از کش شدن فایل
        await response.blob(); // منتظر می‌مانیم تا کل فایل دانلود شود

        const endTime = performance.now();
        const durationInSeconds = (endTime - startTime) / 1000; // مدت زمان به ثانیه

        if (durationInSeconds === 0) {
          console.log('🚀 دانلود آنی بود! سرعت قابل محاسبه نیست.');
          continue;
        }

        const speedBps = fileSizeInBits / durationInSeconds; // سرعت به بیت بر ثانیه
        const speedMbps = speedBps / 1000000; // سرعت به مگابیت بر ثانیه
        const speedMBps = speedMbps / 8;

        console.log(`📥 دانلود از ${baseUrl}:`);
        console.log(`✅ سرعت دانلود: ${speedMbps.toFixed(2)} مگابیت بر ثانیه (Mbps)`);
        console.log(`✅ سرعت دانلود: ${speedMBps.toFixed(2)} مگابایت بر ثانیه (MBps)`);

      } catch (error) {
        console.error(`❌ خطا در ارتباط با سرور ${baseUrl}:`, error.message);
      }

      try {
        const uploadUrl = `http://${baseUrl}/files/upload.php`;
        const fileSizeMB = 5;
        const fileSizeBytes = fileSizeMB * 1024 * 1024;
        const fileSizeBits = fileSizeBytes * 8;

        const fileData = new Blob([new Uint8Array(fileSizeBytes)]);

        const startTime = performance.now();

        const formData = new FormData();
        formData.append('file', fileData, 'upload_test_file.bin');

        const response = await fetch(uploadUrl, {
          method: 'POST',
          body: formData
        });

        const endTime = performance.now();
        const duration = (endTime - startTime) / 1000;

        const speedBps = fileSizeBits / duration;
        const speedMbps = speedBps / 1000000;
        const speedMBps = speedMbps / 8;

        console.log(`⬆️ آپلود به ${baseUrl}:`);
        console.log(`✅ سرعت آپلود: ${speedMbps.toFixed(2)} مگابیت بر ثانیه (Mbps)`);
        console.log(`✅ سرعت آپلود: ${speedMBps.toFixed(2)} مگابایت بر ثانیه (MBps)`);
      } catch (error) {
        console.warn(`❌ خطا در آپلود به ${baseUrl}:`, error);
      }

    }

    console.log('🏁 تست به پایان رسید.');

    await delay(2000); // تاخیر ۲ ثانیه‌ای بین هر سرور


    testButton.classList.remove('active');
    isRotationActive = false;
  }

});
