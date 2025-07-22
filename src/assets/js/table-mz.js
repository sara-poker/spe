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
      console.log(`📡 شروع تست برای سرور: ${baseUrl}`);

      // تست دانلود
      try {
        const downloadUrl = `http://${baseUrl}/files/testfile.bin`;
        const startTime = performance.now();
        const response = await fetch(downloadUrl);
        const reader = response.body.getReader();
        let downloadedSize = 0;
        const chunkSize = 1024;
        let done = false;

        while (!done) {
          const { done: readerDone, value } = await reader.read();
          if (readerDone) break;
          downloadedSize += value.length;
        }

        const endTime = performance.now();
        const totalTime = (endTime - startTime) / 1000; // seconds
        const totalSizeMB = downloadedSize / (1024 * 1024);
        const speedMbps = (totalSizeMB * 8) / totalTime;

        console.log(`⬇️ دانلود از ${baseUrl}:`);
        console.log(`- حجم: ${totalSizeMB.toFixed(2)} MB`);
        console.log(`- زمان: ${totalTime.toFixed(2)} ثانیه`);
        console.log(`- سرعت: ${speedMbps.toFixed(2)} Mbps`);
      } catch (error) {
        console.warn(`❌ خطا در دانلود از ${baseUrl}:`, error);
      }

      // تست آپلود
      try {
        const uploadUrl = `http://${baseUrl}/files/upload.php`;
        const fileData = new Blob([new Uint8Array(5 * 1024 * 1024)]); // 5MB

        const startTime = performance.now();
        const formData = new FormData();
        formData.append('file', fileData, 'upload_test_file.bin');

        const response = await fetch(uploadUrl, {
          method: 'POST',
          body: formData
        });

        const endTime = performance.now();
        const duration = (endTime - startTime) / 1000;
        const speedMbps = (5 * 8) / duration;

        console.log(`⬆️ آپلود به ${baseUrl}:`);
        console.log(`- حجم: 5 MB`);
        console.log(`- زمان: ${duration.toFixed(2)} ثانیه`);
        console.log(`- سرعت: ${speedMbps.toFixed(2)} Mbps`);
      } catch (error) {
        console.warn(`❌ خطا در آپلود به ${baseUrl}:`, error);
      }

      // تست پینگ (شبیه‌سازی‌شده با fetch)
      try {
        const pingHost = 'https://www.google.com'; // شبیه‌سازی
        const pingResults = [];

        for (let i = 0; i < 5; i++) {
          const start = performance.now();
          await fetch(pingHost, { mode: 'no-cors' });
          const end = performance.now();
          pingResults.push(end - start);
          await delay(100);
        }

        const avg = pingResults.reduce((a, b) => a + b, 0) / pingResults.length;
        const jitter = Math.max(...pingResults) - Math.min(...pingResults);

        console.log(`📶 پینگ:`);
        console.log(`- میانگین پینگ: ${avg.toFixed(2)} ms`);
        console.log(`- جیتر: ${jitter.toFixed(2)} ms`);
      } catch (error) {
        console.warn('❌ خطا در تست پینگ:', error);
      }

      // اطلاعات کاربر
      try {
        const userAgent = navigator.userAgent;
        const platform = navigator.platform;
        const language = navigator.language;

        console.log(`🧠 اطلاعات سیستم:`);
        console.log(`- User Agent: ${userAgent}`);
        console.log(`- Platform: ${platform}`);
        console.log(`- Language: ${language}`);
      } catch (error) {
        console.warn('❌ خطا در گرفتن اطلاعات سیستم:', error);
      }

      await delay(2000); // تاخیر ۲ ثانیه‌ای بین هر سرور
    }

    testButton.classList.remove('active');
    isRotationActive = false;
  }

});
