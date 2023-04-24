<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HALG 2023: Registration</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous" />
  <link href="/user/plugins/markdown-notices/assets/notices.css" type="text/css" rel="stylesheet" />
  <link href="/user/plugins/form/assets/form-styles.css" type="text/css" rel="stylesheet" />
  <link href="/user/plugins/login/css/login.css" type="text/css" rel="stylesheet" />
  <link href="/user/themes/halg/css/custom.css" type="text/css" rel="stylesheet" />

  <link href="https://fonts.googleapis.com/css?family=Raleway:400,700" rel="stylesheet" type="text/css" />
  <link href="https://fonts.googleapis.com/css?family=Oswald:400,700" rel="stylesheet" type="text/css" />
  <link href="/styles.css" type="text/css" rel="stylesheet" />
</head>
<body>
  <div class="page-header header-image">
    <div class="page-header__container container">
      <h1 class="page-header__container__title">
        <a href="/index.html">IGAFIT HIGHLIGHTS OF ALGORITHMS</a>
      </h1>
      <p class="page-header__container__location">
        Charles University, Prague, Czech Republic. June 2-4, 2023
      </p>
      <img class="page-header__container__logo" src="/images/halg-logo.svg" />
    </div>
  </div>

  <nav class="navbar navbar-inverse">
    <div class="container">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar_data" aria-expanded="false">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
      </div>
      <div class="collapse navbar-collapse" id="navbar_data">
        <ul class="nav navbar-nav">
          <li>
            <a href="/index.html">
              <span class="glyphicon glyphicon-home glyphicon-large" aria-hidden="true"></span><br>HALG 2023
            </a>
          </li>
          <li>
            <a href="/committee.html">
              <span class="glyphicon glyphicon-info-sign glyphicon-large" aria-hidden="true"></span><br>Committee
            </a>
          </li>
          <li>
            <a href="/call.html">
              <span class="glyphicon glyphicon-bullhorn glyphicon-large" aria-hidden="true"></span><br>Call</a>
          </li>
          <li>
            <a href="/speakers.html">
              <span class="glyphicon glyphicon-user glyphicon-large" aria-hidden="true"></span><br>Invited Speakers</a>
          </li>
          <li>
            <a href="/programme.html">
              <span class="glyphicon glyphicon-time glyphicon-large" aria-hidden="true"></span><br>Programme</a>
          </li>
          <li>
            <a href="/registration">
              <span class="glyphicon glyphicon-pencil glyphicon-large" aria-hidden="true"></span><br>Registration</a>
          </li>
          <li>
            <a href="/venue.html">
              <span class="glyphicon glyphicon-map-marker glyphicon-large" aria-hidden="true"></span><br>Venue</a>
          </li>
          <li>
            <a href="/hotels.html">
              <span class="glyphicon glyphicon-bed glyphicon-large" aria-hidden="true"></span><br>Hotels</a>
          </li>
          <li>
            <a href="/anti-harassment.html">
              <span class="glyphicon glyphicon-exclamation-sign glyphicon-large" aria-hidden="true"></span><br/>Anti-Harassment Policy</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  
  <div class="content">
    <div class="container">
      <h1>Payment status</h1>
      % if payment_successful:
        <div class="form-message form-message--success">
          <h3>Payment successful</h3>
          We have received your payment.
          If you need an invoice or an invitation letter, please <a href="mailto:info@halg.mff.cuni.cz">contact us directly (info@halg.mff.cuni.cz)</a>.
        </div>
      % else:
        <div class="form-message form-message--errors">
          <h3>Payment unsuccessful</h3>
          We have not managed to verify your payment.
          If the payment gate informed you that it succeeded, please <a href="mailto:info@halg.mff.cuni.cz">contact us (info@halg.mff.cuni.cz)</a>.
        </div>
    </div>

    <div class="container">
      <footer class="footer">
        <p>&copy; IGAFIT Highlights of Algorithms 2023</p>
        <p>If you have any questions regarding HALG 2023, please contact us via the following email address: <a href="mailto:info@halg.mff.cuni.cz">info@halg.mff.cuni.cz</a>.</p>
      </footer>
    </div>
  </div>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</body>
</html>
