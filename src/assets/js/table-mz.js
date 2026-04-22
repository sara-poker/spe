$(async function() {
  const dt_basic_table = $('.datatables-basic');
  const testButton = document.getElementById('testButton');
  testButton.disabled = true;

  try {
    const parser = new UAParser();
    const result = parser.getResult();

    document.getElementById('browser').innerText = `${result.browser.name} | ${result.browser.version}`;
    document.getElementById('os').innerText = `${result.os.name} | ${result.os.version}`;
    document.getElementById('device').innerText = `${result.device.type || 'Desktop'} | ${result.device.vendor || 'Unknown'} | ${result.device.model || 'Unknown'}`;
    document.getElementById('cpu').innerText = result.cpu.architecture || 'Unknown';

    const ipInfoRes = await fetch('https://ipapi.co/json');
    const ipInfo = await ipInfoRes.json();
    const countrySlug = ipInfo.country_name.toLowerCase().replace(/\s+/g, '');

    document.getElementById('ip').innerText = ipInfo.ip;
    document.getElementById('country').innerText = ipInfo.country_name;
    document.getElementById('city').innerText = ipInfo.city;
    document.getElementById('isp').innerText = ipInfo.org;
    document.getElementById('flag').src = `/static/img/flag/${countrySlug}.png`;

    const logoFile = `${ipInfo.asn}.png`;
    document.getElementById('isp-logo').src = `/static/img/ispLogo/RGB/${logoFile}`;
  } catch (error) {
    console.error('⚠️ خطا در دریافت اطلاعات کاربر:', error);
  }

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
            const countrySlug = data.toLowerCase().replace(/\s+/g, '');
            return `<img alt="${data}" src="/static/img/flag/${countrySlug}.png" width="32" class="me-1" style="vertical-align: middle;">`;
          }
        },
        { data: 'name', title: 'نام سرور' },
        { data: 'ip', title: 'IP' },
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
      if (isRunning || testButton.disabled) return;

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

      startSpeedTest(selectedServers);
    });
  }

  async function testMetrics(host, count = 5) {
    const success_times = [];
    let failed_count = 0;
    const noCacheUrl = `${host}?t=${new Date().getTime()}`;

    for (let i = 0; i < count; i++) {
      const start = performance.now();
      try {
        await fetch(noCacheUrl, { method: 'HEAD', cache: 'no-store', mode: 'no-cors' });
        const duration = performance.now() - start;
        success_times.push(duration);
      } catch {
        failed_count++;
      }
    }

    if (success_times.length > 0) {
      const avg_ping = success_times.reduce((a, b) => a + b, 0) / success_times.length;
      const jitter = Math.max(...success_times) - Math.min(...success_times);
      const packet_loss = (failed_count / count) * 100;

      return {
        avg_ping: Math.round(avg_ping),
        jitter: Math.round(jitter),
        packet_loss: Math.round(packet_loss)
      };
    } else {
      return { avg_ping: 0, jitter: 0, packet_loss: 100 };
    }
  }

  try {
    const metrics = await testMetrics('https://www.cloudflare.com', 5);

    document.getElementById('ping').innerText = `${metrics.avg_ping} ms`;
    document.getElementById('jitter').innerText = `${metrics.jitter} ms`;
    document.getElementById('packet').innerText = `${metrics.packet_loss}%`;
    testButton.disabled = false;
  } catch (err) {
    console.error('⚠️ خطا در تست پینگ:', err);
  }

  function createAccordionItem({ country, ip, downloadMbps, downloadMBps, uploadMbps, uploadMBps, name, isFirst }) {
    const countrySlug = country.toLowerCase().replace(/\s+/g, '');
    const flagUrl = `/static/img/flag/${countrySlug}.png`;
    const accordionId = `accordion-${ip.replace(/\./g, '-')}`;

    return `
    <div class="accordion-item card">
      <h2 class="accordion-header text-body d-flex justify-content-between" id="${accordionId}-header">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#${accordionId}" aria-controls="${accordionId}">
          <img alt="${country}" src="${flagUrl}" width="32">
          <div class="ps-3">${name}</div>
          <div class="ps-3">|</div>
          <div class="ps-3">${ip}</div>
        </button>
      </h2>
      <div id="${accordionId}" class="accordion-collapse collapse ${isFirst ? 'show' : ''}" data-bs-parent="#accordionIcon">
        <div class="accordion-body">
          <div class="row">
            <div class="col-md-6 mb-4">
              <div class="p-3 rounded shadow-sm border">
                <h5 class="fw-bold mb-3 text-primary">⬇️ دانلود</h5>
                <div class="d-flex justify-content-between mb-2">
                  <span class="text-muted">سرعت دانلود (Mbps):</span>
                  <span class="fw-semibold">${downloadMbps}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-muted">سرعت دانلود (MBps):</span>
                  <span class="fw-semibold">${downloadMBps}</span>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-4">
              <div class="p-3 rounded shadow-sm border">
                <h5 class="fw-bold mb-3 text-success">⬆️ آپلود</h5>
                <div class="d-flex justify-content-between mb-2">
                  <span class="text-muted">سرعت آپلود (Mbps):</span>
                  <span class="fw-semibold">${uploadMbps}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-muted">سرعت آپلود (MBps):</span>
                  <span class="fw-semibold">${uploadMBps}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    `;
  }

  const accordionContainer = document.getElementById('accordionIcon');

  async function startSpeedTest(selectedServers) {
    const urls = selectedServers.map(server => server.url);
    if (isRotationActive) return;

    isRotationActive = true;
    testButton.classList.add('active');
    accordionContainer.innerHTML = '';

    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    for (const server of selectedServers) {
      let baseUrl = server.url;
      const ip = baseUrl;
      console.log(`شروع تست ${server.name} >>`);
      const country = server.country;
      const name = server.name;
      let downloadMbps = 'خطا';
      let downloadMBps = 'خطا';
      let uploadMbps = 'خطا';
      let uploadMBps = 'خطا';

      try {
        const fileSizeInBits = 20971520 * 8;
        const startTime = performance.now();
        const response = await fetch(`https://${baseUrl}/files/testfile.bin`, { cache: 'no-store' });
        await response.blob();
        const endTime = performance.now();
        const duration = (endTime - startTime) / 1000;

        downloadMbps = (fileSizeInBits / duration / 1000000).toFixed(2);
        downloadMBps = (downloadMbps / 8).toFixed(2);
        console.log(`پایان دانلود ${server.name} >>`);
      } catch (err) {
        console.error(`خطا در دانلود از ${baseUrl}:`, err);
      }

      try {
        const uploadUrl = `https://${baseUrl}/files/upload.php`;
        const fileSizeBytes = 5 * 1024 * 1024;
        const fileSizeBits = fileSizeBytes * 8;
        const fileData = new Blob([new Uint8Array(fileSizeBytes)]);
        const formData = new FormData();
        formData.append('file', fileData, 'upload_test_file.bin');

        const startTime = performance.now();
        await fetch(uploadUrl, { method: 'POST', body: formData });
        const endTime = performance.now();
        const duration = (endTime - startTime) / 1000;

        uploadMbps = (fileSizeBits / duration / 1000000).toFixed(2);
        uploadMBps = (uploadMbps / 8).toFixed(2);
        console.log(`پایان آپلود ${server.name} >>`);
      } catch (err) {
        console.error(`خطا در آپلود به ${baseUrl}:`, err);
      }

      accordionContainer.innerHTML += createAccordionItem({
        country: country || 'france',
        ip,
        downloadMbps,
        downloadMBps,
        uploadMbps,
        uploadMBps,
        name,
        isFirst: selectedServers.indexOf(server) === 0
      });

      await delay(2000);
    }

    testButton.classList.remove('active');
    isRotationActive = false;
  }
});
