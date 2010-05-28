##########################################################################
#
#  Copyright (c) 2010, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of Image Engine Design nor the names of any
#       other contributors to this software may be used to endorse or
#       promote products derived from this software without specific prior
#       written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import maya.cmds
import maya.OpenMaya

import IECore
import IECoreGL
import IECoreMaya

class FnProceduralHolderTest( IECoreMaya.TestCase ) :

	class SphereProcedural( IECore.ParameterisedProcedural ) :
	
		def __init__( self ) :
		
			IECore.ParameterisedProcedural.__init__( self, "" )
			
			self.parameters().addParameters(
				
				[
					IECore.FloatParameter(
						"radius",
						"",
						1.0,
					),
				]
			
			)
			
		def doBound( self, args ) :
		
			result = IECore.Box3f( IECore.V3f( -args["radius"].value ), IECore.V3f( args["radius"].value ) )
			return result
			
		def doRender( self, renderer, args ) :
			
			renderer.sphere( args["radius"].value, -1, 1, 360, {} )
			
		def doRenderState( self, renderer, args ) :
			
			pass

	def testScene( self ) :

		node = maya.cmds.createNode( "ieProceduralHolder" )

		fnPH = IECoreMaya.FnProceduralHolder( node )
		fnPH.setParameterised( self.SphereProcedural() )
		
		radiusAttr = fnPH.parameterPlugPath( fnPH.getProcedural()["radius"] )
		
		prevScene = None
		for i in range( 0, 10000 ) :
		
			maya.cmds.setAttr( radiusAttr, i )
			scene = fnPH.scene()
			self.failUnless( isinstance( scene, IECoreGL.Scene ) )
			self.failIf( prevScene is not None and scene.isSame( prevScene ) )
			prevScene = scene
			
if __name__ == "__main__":
	IECoreMaya.TestProgram()