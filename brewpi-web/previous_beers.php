<?php
/* Copyright 2012 BrewPi/Elco Jacobs.
 * This file is part of BrewPi.

 * BrewPi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * BrewPi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with BrewPi.  If not, see <http://www.gnu.org/licenses/>.
 */
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<title>BrewPi: previous beers</title>
</head>
<body>
	<div id="beer-selector">
		<span>Select the beer you would like to view:</span>
		<select id="prev-beer-name">
			<?php
				foreach(glob('data/*', GLOB_ONLYDIR) as $dir)
				{
					$dir = basename($dir);
					if($dir !== "profiles"){
					    echo '<option value="', $dir, '">', urldecode($dir), '</option>';
					}
				}
			?>
		</select>
		<button id="prev-beer-show">Show</button>
		<button id="download-csv">Download CSV</button>
	</div>
	<div class="chart-container">
			<div id="prev-beer-chart-label" class="beer-chart-label"></div>
		<div id="prev-beer-chart" class="beer-chart" style="width:770px; height:500px"></div>
		<div id="prev-beer-chart-controls" class="beer-chart-controls" style="display: none">
		    <div id="curr-beer-chart-buttons" class="beer-chart-buttons">
		    	<div class="beer-chart-legend-row">
					<button class="chart-help" title="Help"></button>
		    		<div class="beer-chart-legend-label">Help</div>
	    			<br class="crystal" />
		    	</div>
			</div>
		    <div id="curr-beer-chart-legend" class="beer-chart-legend">
		    	<div class="beer-chart-legend-row time">
		    		<div class="beer-chart-legend-time">Date/Time</div>
		    	</div>
		    	<div class="beer-chart-legend-row beerTemp">
		    		<div class="toggle beerTemp" onClick="toggleLine(this)"></div>
		    		<div class="beer-chart-legend-label" onClick="toggleLine(this)">Beer Temp</div>
		    		<div class="beer-chart-legend-value">--</div>
		    		<br class="crystal" />
		    	</div>
		    	<div class="beer-chart-legend-row beerSet">
					<div class="toggle beerSet" onClick="toggleLine(this)"></div>
		    		<div class="beer-chart-legend-label" onClick="toggleLine(this)">Beer Setting</div>
		    		<div class="beer-chart-legend-value">--</div>
		    		<br class="crystal" />
		    	</div>
		    	<div class="beer-chart-legend-row fridgeTemp">
					<div class="toggle fridgeTemp" onClick="toggleLine(this)"></div>
		    		<div class="beer-chart-legend-label" onClick="toggleLine(this)">Fridge Temp</div>
		    		<div class="beer-chart-legend-value">--</div>
		    		<br class="crystal" />
		    	</div>
		    	<div class="beer-chart-legend-row fridgeSet">
					<div class="toggle fridgeSet" onClick="toggleLine(this)"></div>
		    		<div class="beer-chart-legend-label" onClick="toggleLine(this)">Fridge Setting</div>
		    		<div class="beer-chart-legend-value">--</div>
		    		<br class="crystal" />
		    	</div>
		    	<div class="beer-chart-legend-row log1Temp">
					<div class="toggle log1Temp" onClick="toggleLine(this)"></div>
		    		<div class="beer-chart-legend-label" onClick="toggleLine(this)">Log1 Temp</div>
		    		<div class="beer-chart-legend-value">--</div>
		    		<br class="crystal" />
		    	</div>
					<div class="beer-chart-legend-row log2Temp">
					<div class="toggle log2Temp" onClick="toggleLine(this)"></div>
		    		<div class="beer-chart-legend-label" onClick="toggleLine(this)">Log2 Temp</div>
		    		<div class="beer-chart-legend-value">--</div>
		    		<br class="crystal" />
		    	</div>
					<div class="beer-chart-legend-row log3Temp">
					<div class="toggle log3Temp" onClick="toggleLine(this)"></div>
		    		<div class="beer-chart-legend-label" onClick="toggleLine(this)">Log3 Temp</div>
		    		<div class="beer-chart-legend-value">--</div>
		    		<br class="crystal" />
		    	</div>
                <!-- Tilt Hydrometer lines -->
                <div class="beer-chart-legend-row redTemp">
                    <div class="toggle redTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Red Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row redSG">
                    <div class="toggle redSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Red Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row greenTemp">
                    <div class="toggle greenTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Green Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row greenSG">
                    <div class="toggle greenSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Green Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row blackTemp">
                    <div class="toggle blackTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Black Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row blackSG">
                    <div class="toggle blackSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Black Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row purpleTemp">
                    <div class="toggle purpleTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Purple Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row purpleSG">
                    <div class="toggle purpleSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Purple Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row orangeTemp">
                    <div class="toggle orangeTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Orange Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row orangeSG">
                    <div class="toggle orangeSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Orange Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row blueTemp">
                    <div class="toggle blueTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Blue Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row blueSG">
                    <div class="toggle blueSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Blue Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row yellowTemp">
                    <div class="toggle yellowTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Yellow Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row yellowSG">
                    <div class="toggle yellowSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Yellow Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row pinkTemp">
                    <div class="toggle pinkTemp" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Pink Tilt Temp</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <div class="beer-chart-legend-row pinkSG">
                    <div class="toggle pinkSG" onClick="toggleLine(this)"></div>
                    <div class="beer-chart-legend-label" onClick="toggleLine(this)">Pink Tilt SG</div>
                    <div class="beer-chart-legend-value">--</div>
                    <br class="crystal" />
                </div>
                <!-- Tilt Hydrometer lines END-->
		    	<div class="beer-chart-legend-row state">
					<div class="state-indicator"></div>
		    		<div class="beer-chart-legend-label"></div>
		    		<br class="crystal" />
		    	</div>
		    	<div class="beer-chart-legend-row annotation last">
					<div class="toggleAnnotations dygraphDefaultAnnotation" onClick="toggleAnnotations(this)">A</div>
		    		<div class="beer-chart-legend-label" onClick="toggleAnnotations(this)">Annotations</div>
		    		<br class="crystal" />
		    	</div>
		    </div>
		</div>
	</div>
	<script>
		$(document).ready(function(){
			$("button#prev-beer-show").button({ icons: {primary: "ui-icon-circle-triangle-e"} }).click(function(){
				drawBeerChart(String($("select#prev-beer-name").val()), "prev-beer-chart" );
			});
			$("button#download-csv").button({ icons: {primary: "ui-icon-arrowthickstop-1-s"} }).click(function(){
				var url = "data/" + String($("select#prev-beer-name").val()) + "/" + String($("select#prev-beer-name").val()) + ".csv";
				window.open(encodeURI(url), 'Download CSV' );
			});
			$("#prev-beer-chart-controls button.chart-help").button({	icons: {primary: "ui-icon-help" }, text: false }).click(function(){
				$("#chart-help-popup").dialog("open");
			});
		});
	</script>
</body>
</html>
