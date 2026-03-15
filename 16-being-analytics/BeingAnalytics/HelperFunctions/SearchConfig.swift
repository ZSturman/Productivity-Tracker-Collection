//
//  SearchConfig.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/18/23.
//

import Foundation
import SwiftUI


struct SearchConfig: Equatable {
    enum Filter {
        case all, action, state
    }
    var query: String = ""
    var filter: Filter = .all
}

enum Sort {
    case asc, desc
}
