//
//  SharedVM.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation
import SwiftUI

class SharedVM: ObservableObject {
    @Published var actionStates: [ActionState] = []
    
}
