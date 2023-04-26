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
      <h1>Registration</h1>

      <p>Early registration (by 21st May 2023)</p>
      <ul>
        <li>Students: 2600 CZK</li>
        <li>Non-students: 3500 CZK</li>
      </ul>
      <p>Late registration</p>
      <ul>
        <li>Students: 4000 CZK</li>
        <li>Non-students: 5000 CZK</li>
      </ul>
      <p>On-site registration: 6000 CZK</p>


      <h2 id="registration-form">Registration form</h2>
      <form id="registration-form" name="registrationForm" action="#registration-form" method="post" accept-charset="utf-8">
        % if 'errors' in locals():
          % if len(errors) > 0:
            <div class="form-message form-message--errors">
              <h3>Errors</h3>
              <ul>
                % for error in errors:
                <li>{{error}}</li>
                % end
              </ul>
            </div>
          % else:
            <div class="form-message form-message--success">
              <h3>Success</h3>
              You will be redirected to the payment gate soon (10 seconds).
              If nothing happens, please click the following link.
              <a href="{{payment_url}}">Link to payment gate.</a>
            </div>
            <script>
            setTimeout(function() {
              window.location.href = "{{payment_url}}"
            }, 10000)
            </script>
          % end
        % end
        <div class="input-group">
          <label for="name">First name (required):</label>
          <input type="text" id="name" name="name" required />
        </div>

        <div class="input-group">
          <label for="name">Surname:</label>
          <input type="text" id="surname" name="surname" />
        </div>

        <div class="input-group">
          <label for="email">Email address (required):</label>
          <input type="email" id="email" name="email" required />
        </div>

        <div class="input-group">
          <label for="affiliation">Affiliation:</label>
          <input type="text" id="affiliation" name="affiliation" />
        </div>

        <div class="input-group">
          <label for="address">Address (street etc.) (required):</label>
          <input type="text" id="address" name="address" required />
        </div>

        <div class="input-group">
          <label for="city">City (required):</label>
          <input type="text" id="city" name="city" required />
        </div>

        <div class="input-group">
          <label for="country">Country (required):</label>
          <input type="text" id="country" name="country" required />
        </div>

        <div class="input-group">
          <label for="zip-code">ZIP Code:</label>
          <input type="text" id="zip-code" name="zipCode" />
        </div>

        <div class="input-group">
          <label for="vat-tax-no">VAT/TAX no.:</label>
          <input type="text" id="vat-tax-no" name="vatTaxNo" />
        </div>

        <div class="input-group">
          <div>I am registering as a student.</div>
          <div>
            <input type="checkbox" id="is-student" name="isStudent" />
            <label for="is-student">Yes</label>
          </div>
        </div>

        <div class="input-group">
          <label for="remarks">Remarks for the organizers:</label>
          <textarea id="remarks" name="remarks"></textarea>
        </div>

        <input type="submit" value="Register" />
      </form>
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
