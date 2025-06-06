# This script takes the talkgroups list and creates a playlist config file for SDRTrunk. 
# Talkgroups of interest are set up with action scripts and then every other talkgroup is muted. 
# This config is specific to Indianapolis, Indiana and would require changes for other locations, specifically
# the frequency entries in the channel section.

from talkgroups import talkgroups

print('<playlist version="4">')
for id, name in talkgroups:
    alias = f"""<alias color="0" name="{name}" group="Indianapolis Metropolitan Police Department (IMPD)" list="IMPD">
    <id type="talkgroup" value="{id}" protocol="APCO25"/>
    <action type="scriptAction" interval="DELAYED_RESET" period="5">
      <script>/code/notifier/log_scripts/log_activity_{id}.sh</script>
    </action>
  </alias>"""
    print(alias)
print("""
 <alias color="0" name="Everything Else" list="IMPD">
    <id type="priority" priority="-1"/>
    <id type="talkgroupRange" protocol="APCO25" min="1" max="65535"/>
  </alias>
<channel system=" Metropolitan Emergency Services Agency (MESA) (Formerly IDPS) " site="Marion County Public Safety (System 1) " enabled="true" order="1">
    <alias_list_name>IMPD</alias_list_name>
    <event_log_configuration>
      <logger>CALL_EVENT</logger>
      <logger>DECODED_MESSAGE</logger>
      <logger>TRAFFIC_CALL_EVENT</logger>
      <logger>TRAFFIC_DECODED_MESSAGE</logger>
    </event_log_configuration>
    <source_configuration type="sourceConfigTunerMultipleFrequency" preferred_tuner="RTL-2832/R820T 00000001" frequency_rotation_delay="400" source_type="TUNER_MULTIPLE_FREQUENCIES">
      <frequency>856162500</frequency>
      <frequency>856512500</frequency>
      <frequency>857662500</frequency>
      <frequency>858187500</frequency>
    </source_configuration>
    <aux_decode_configuration/>
    <decode_configuration type="decodeConfigP25Phase1" modulation="C4FM" traffic_channel_pool_size="20" ignore_data_calls="false"/>
    <record_configuration/>
  </channel>
</playlist>""")
