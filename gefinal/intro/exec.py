
<div class="tab" id="instructions_9" style="display: none">
    <div class="card">
        <h5 class="card-header">How is the firms' profit calculated?</h5>
        <div class="card-body">
           <p class="block-sentence">
                The firms' profit in each round is determined by the wage they pay to all their workers, the effort you provide to them, the effort other workers provide, and the number of workers they employ.
               If they <b>do not employ any workers</b> in a round, they will earn a profit of {{ outside_option_employers_points_tokens }} {{ currency_plural }} in that round.
           </p>
            <p class="block-sentence">
                If they employ at least one worker, their profit will be the difference between the revenue they gain from worker effort choices and the wage they pay to all workers:
            </p>
            <p style="margin-left: 50px;">
                <b>Profit = Total revenue – total wage payments</b>.
            </p>

            <div class="container">
              <table>
                <tr>
                  <th colspan="3">Worker Effort and Revenue</th>
                </tr>
                <tr>
                  <th>Case</th>
                  <th>Revenue per worker</th>
                  <th>Total revenue</th>
                </tr>
                <tr>
                  <td>Employ two workers. Both workers chose High effort</td>
                  <td>140</td>
                  <td>280</td>
                </tr>
                <tr>
                  <td>Employ two workers. One worker chooses High effort and the other chooses Low effort</td>
                  <td>77</td>
                  <td>154</td>
                    </div>
                </div>
                </tr>
            <tr>
              <td>Employ two workers. Both workers chose Low effort</td>
              <td>14</td>
              <td>28</td>
            </tr>
            <tr>
              <td>Employ one worker. The worker chooses High effort</td>
              <td>160</td>
              <td>160</td>
            </tr>
            <tr>
              <td>Employ one worker. The worker chooses Low effort</td>
              <td>16</td>
              <td>16</td>
            </tr>
          </table>
        </div>

    <br>
  <p>
        <button type="button" class="btn-tab btn-secondary" data-offset="1" onclick="MoveToPrevious(this)">Previous</button>
        <button type="button" class="btn-tab btn-secondary" data-offset="1" onclick="MoveToNext(this); ChangeHeader();" style="float: right;">Next</button>
    </p>
</div>

