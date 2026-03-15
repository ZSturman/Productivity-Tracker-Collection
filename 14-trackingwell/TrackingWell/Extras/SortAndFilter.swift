//
//  SortAndFilter.swift
//  TrackingWell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation

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
