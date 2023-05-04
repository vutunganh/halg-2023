<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HALG 2023: Participants</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous" />

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
          <li class="active_nav">
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
      <h1>Participants</h1>

      <table class="participants-table">
        <thead>
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Surname</th>
            <th>Email address</th>
            <th>Affiliation</th>
            <th>Address</th>
            <th>City</th>
            <th>Country</th>
            <th>ZIP code</th>
            <th>VAT/TAX no.</th>
            <th>Is student?</th>
            <th>Date registered</th>
            <th>Has paid?</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody>
          % for p in participants:
            <tr>
              <td>{{p.id}}</td>
              <td>{{p.name}}</td>
              <td>{{p.surname}}</td>
              <td>{{p.email}}</td>
              <td>{{p.affiliation}}</td>
              <td>{{p.address}}</td>
              <td>{{p.city}}</td>
              <td>{{p.country}}</td>
              <td>{{p.zip_code}}</td>
              <td>{{p.vat_tax_no}}</td>
              <td>{{p.is_student}}</td>
              <td>{{p.date_registered}}</td>
              <td>{{p.has_paid}}</td>
              <td>{{p.remarks}}</td>
            </tr>
          % end
        </tbody>
      </table>

    </div>
  </div>

  <div class="container">
    <footer class="footer">
      <p>&copy; IGAFIT Highlights of Algorithms 2023</p>
      <p>If you have any questions regarding HALG 2023, please contact us via the following email address: <a href="mailto:info@halg.mff.cuni.cz">info@halg.mff.cuni.cz</a>.</p>
    </footer>
  </div>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</body>
</html>
