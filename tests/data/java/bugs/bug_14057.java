/*
Copyright 2009-2010 Igor Polevoy

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package org.javalite.common.test;

import org.junit.Test;

import static org.javalite.test.jspec.JSpec.a;

/**
 * @author Igor Polevoy
 */
public class ExpectationTest {

    @Test
    public void shouldTestSuperClassAndInterface(){

        class Car{}
        class Toyota extends Car{}

        a(new Car()).shouldBeA(Car.class);
        a(new Toyota()).shouldBeA(Car.class);

        class Job implements Runnable{
            public void run() {}
        }

        a(new Job()).shouldBeA(Runnable.class);
    }
}
