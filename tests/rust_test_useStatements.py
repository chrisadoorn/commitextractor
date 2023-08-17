#test file voor use statements
from src.Rust.utils import CleanUpDiffText, parseText,CleanUpFullText
from src.models.extracted_data_models import BestandsWijziging, open_connection
from pyparsing import QuotedString, cppStyleComment, rest_of_line

script = """use std::path::{Path, PathBuf};
//SL COMMENT1

use rustc_//SL COMMENT2serialize::json::{Json};
use lua::{/// SL COMMENT3State, ThreadStatus, Type};
use self:://!SL COMMENT4 input::Input;
use config::"SL LITERAL1;"
use shared::'SL LITERAL2'
use config::"SL LITERAL1;" WWW;
use shared::'SL LITERAL2'{Id, Peer};

mod1 /* ML COMMENT input;
mod main;*/ mod1
mod lua_json;

/*pub1 ML COMMENT2 use self::main::{spawn, Settings};*/
    /*pub1 ML COMMENT2 use self::main::{spawn, Settings};*/
pub1 /*pub1 ML COMMENT2 use self::main::{spawn, Settings};*/

/*pub2 ML COMMENT3 
    use self::main::{spawn, Settings};*/
        /*pub2 ML COMMENT3 
    use self::main::{spawn, Settings};*/
    
    /*pub2 ML COMMENT3 
use self::main::{spawn, Settings};*/
    
pub2 /*pub2 ML COMMENT3 
    use self::main::{spawn, Settings};*/
    
pub3 /* ML COMMENT4 use self::main::{spawn, Settings};

            */pub rest3 
pub4 /* ML COMMENT4 use self::main::{spawn, Settings};       */ pub rest4 
    
    pub struct Scheduler {
    hostname: String, 
    lua: State,
    previous_schedule_hash: Option<String>,
}

quick_"ML LITERALerror! {
    #[derive(Debug)]"
quick_"ML LITERAL2error! {
    #[derive(Debug)]" xxxxxxx;
    
quick_'ML LITERAL3error! {
    #[derive(Debug)]'
quick_'ML LITERAL4error! {
    #[derive(Debug)]' xxxxxxx;
"""

#commentparser = cppStyleComment
#multilineparser = QuotedString("'", multiline=True) | QuotedString('"', multiline=True)

#text = (multilineparser.suppress().transform_string(CleanUpFullText(script)))

print(parseText(script))
"""
output_text1 = CleanUpFullText(script)
print("output_text1 \n" + output_text1)

output_text2 = parseText(output_text1)
print("output_text2 \n" + output_text2)
"""





































"""
output_text3 = transform_use(output_text2)
print("output_text3 \n" + output_text3)

#output_text4 = transformDiffText(script)
#print("eigen trans \n" + output_text4)


#print("andere trans \n" + __opkuizen_speciale_tekens(output_text4, True))

#print(commentparser.suppress().transform_string(multilineparser.suppress().transform_string(singlelineparser.suppress().transform_string(script))))
"""

"""
open_connection()  # nodig bij gebruik PooledPostgresqlExtDatabase
print ("open_connection()")
bestandswijzigingen_lijst = BestandsWijziging.select(BestandsWijziging.id, BestandsWijziging.difftext).where(BestandsWijziging.id < 1000000)
print ("bestandswijzigingen_lijst()")

for bestandswijziging in bestandswijzigingen_lijst:
        print("BestandsWijziging.id "+ str(bestandswijziging.id))
        #print(transformDiffText(bestandswijziging.difftext))
        CleanUpDiffText(bestandswijziging.difftext)
"""